"""
Offline verification harness (not shipped with the app).
Exercises build_duckdb's generation code without DuckDB by faking the connection,
then checks relational integrity + aggregations with pandas.
"""
import re
import sys
import types
sys.modules["duckdb"] = types.ModuleType("duckdb")  # stub: builder imports it
import pandas as pd
import build_duckdb as b


class FakeCon:
    def __init__(self):
        self.tables = {}
        self.seqs = {}

    def execute(self, sql):
        m = re.search(r"nextval\('([^']+)'\)", sql)
        if m:
            name = m.group(1)
            self.seqs[name] = self.seqs.get(name, 0) + 1
            self._last = self.seqs[name]
        else:
            self._last = None
        return self

    def fetchone(self):
        return (self._last,)

    def executemany(self, sql, rows):
        m = re.search(r"INSERT INTO (\w+)", sql)
        if not m:                       # e.g. the void UPDATE — ignore here
            return
        self.tables.setdefault(m.group(1), []).extend(rows)


con = FakeCon()
b.load_reference(con)
n_o, n_i, n_m, n_v = b.generate_orders(con)

cols = {
    "stores": ["store_id", "store_name", "city", "state"],
    "menu_categories": ["category_id", "category_name", "sort_order"],
    "sizes": ["size_id", "size_name", "sort_order"],
    "menu_items": ["item_id", "category_id", "item_name", "description", "is_secret_menu"],
    "item_prices": ["item_id", "size_id", "price"],
    "modifiers": ["modifier_id", "modifier_name", "description", "price_delta", "applies_to"],
    "combos": ["combo_id", "combo_name", "burger_item_id", "description", "price"],
    "orders": ["order_id", "transaction_id", "store_id", "order_ts", "order_type",
               "payment_method", "subtotal", "tax_rate", "tax_amount", "total"],
    "order_items": ["order_item_id", "order_id", "item_id", "combo_id", "size_id",
                    "quantity", "unit_price", "line_total"],
    "order_item_modifiers": ["order_item_id", "modifier_id", "price_delta"],
}
df = {t: pd.DataFrame(con.tables.get(t, []), columns=c) for t, c in cols.items()}

print(f"orders={n_o}  order_items={n_i}  order_item_modifiers={n_m}  "
      f"voided={n_v}")

# 1. Referential integrity --------------------------------------------------
assert df["order_items"]["order_id"].isin(df["orders"]["order_id"]).all(), "FK order_id"
oi = df["order_items"]
items_ok = oi["item_id"].dropna().isin(df["menu_items"]["item_id"]).all()
combo_ok = oi["combo_id"].dropna().isin(df["combos"]["combo_id"]).all()
assert items_ok and combo_ok, "FK item/combo"
assert oi["size_id"].isin(df["sizes"]["size_id"]).all(), "FK size"
assert df["order_item_modifiers"]["order_item_id"].isin(oi["order_item_id"]).all(), "FK oim"
# CHECK: each line is item XOR-ish combo (at least one present)
assert (oi["item_id"].notna() | oi["combo_id"].notna()).all(), "CHECK item/combo"
assert df["transaction_id"] if False else df["orders"]["transaction_id"].is_unique, "txn unique"
print("OK referential integrity + unique transaction_id")

# 2. Order totals consistent (subtotal == sum of line_totals) ---------------
line_sum = oi.groupby("order_id")["line_total"].sum().round(2)
merged = df["orders"].set_index("order_id")["subtotal"].round(2)
assert (line_sum.sort_index().values == merged.sort_index().values).all(), "subtotal mismatch"
tax_diff = ((df["orders"]["subtotal"] * b.TAX_RATE) - df["orders"]["tax_amount"]).abs()
assert (tax_diff <= 0.01).all(), "tax mismatch"
assert ((df["orders"]["subtotal"] + df["orders"]["tax_amount"]
         - df["orders"]["total"]).abs() <= 0.001).all(), "total mismatch"
print("OK subtotal/tax/total arithmetic")

# 3. Sample analytics (the kind the dashboard will run) ---------------------
rev = df["orders"]["total"].sum()
print(f"\nTotal revenue over {b.DAYS_OF_HISTORY} days: ${rev:,.2f}")
print(f"Avg order value: ${df['orders']['total'].mean():.2f}")

print("\nTop 5 menu items by qty (join order_items -> menu_items):")
top = (oi.dropna(subset=["item_id"])
         .merge(df["menu_items"], on="item_id")
         .groupby("item_name")["quantity"].sum()
         .sort_values(ascending=False).head(5))
print(top.to_string())

print("\nOrders & revenue by store:")
rs = (df["orders"].merge(df["stores"], on="store_id")
        .groupby(["store_id", "store_name"])
        .agg(orders=("order_id", "count"), revenue=("total", "sum"))
        .sort_index())
print(rs.round(2).to_string())
assert dict(rs["orders"].droplevel(1)) == b.STORE_ORDER_COUNTS, \
    "per-store counts mismatch"
print("OK per-store order counts match STORE_ORDER_COUNTS")

print("\nMost-used modifiers:")
mm = (df["order_item_modifiers"].merge(df["modifiers"], on="modifier_id")
        .groupby("modifier_name").size().sort_values(ascending=False).head(5))
print(mm.to_string())
print("\nALL CHECKS PASSED")
