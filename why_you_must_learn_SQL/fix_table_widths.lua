-- Pandoc Lua filter: give every table explicit column widths, proportional
-- to the longest content in each column, instead of pandoc's default (equal
-- widths based on the markdown separator row, which ignores actual content).
-- Without this, LaTeX output can overlap columns when one column holds long
-- inline code (e.g. `customers.customer_id`) and another holds prose.

local function cell_text_len(cell)
  local len = 0
  for _, blk in ipairs(cell.contents) do
    local s = pandoc.utils.stringify(blk)
    if #s > len then len = #s end
  end
  return len
end

-- Inline code (e.g. `products.product_id`) has no spaces or hyphens, so
-- LaTeX has no break point and just overflows the cell no matter how wide
-- the column is. \seqsplit (from the seqsplit package) allows a break
-- between any two characters, as a last resort, only inside table cells.
local function breakable_code(cell)
  return pandoc.walk_block(cell, {
    Code = function(c)
      if FORMAT == "latex" then
        return pandoc.RawInline("latex", "\\seqsplit{" .. c.text:gsub("([%%#&_{}])", "\\%1") .. "}")
      end
    end
  })
end

function Table(tbl)
  local ncols = #tbl.colspecs
  local maxlen = {}
  for i = 1, ncols do maxlen[i] = 1 end

  local function scan(body_rows)
    for _, row in ipairs(body_rows) do
      for i, cell in ipairs(row.cells) do
        local l = cell_text_len(cell)
        if l > maxlen[i] then maxlen[i] = l end
        for j, blk in ipairs(cell.contents) do
          cell.contents[j] = breakable_code(blk)
        end
      end
    end
  end

  if tbl.head and tbl.head.rows then scan(tbl.head.rows) end
  for _, body in ipairs(tbl.bodies) do
    if body.body then scan(body.body) end
  end

  -- Cap the longest column's influence so one wide code cell doesn't crush
  -- the rest of the table, then normalize to sum to 1.
  local total = 0
  for i = 1, ncols do
    maxlen[i] = math.min(maxlen[i], 40)
    total = total + maxlen[i]
  end

  local new_colspecs = {}
  for i = 1, ncols do
    local align = tbl.colspecs[i][1]
    local width = maxlen[i] / total
    new_colspecs[i] = { align, width }
  end
  tbl.colspecs = new_colspecs
  return tbl
end
