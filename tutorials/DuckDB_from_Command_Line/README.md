# DuckDB from the Command Line: Start Here

**OMIS 105 - Fall 2026. Reviewed October 2, 2026.**

This folder teaches the standalone **DuckDB CLI**: a program you run in a
terminal. No Python, virtual environment, Marimo, server, or DuckDB account
is needed. The examples use **DuckDB 1.5.5**; installers may provide a newer
stable version. Do not select a preview release for this lesson.

## Choose Your Guide

| Your computer | Readable Markdown |
|---|---|
| Mac | [macOS guide](duckdb_from_command_line_on_macbook.md) |
| Windows | [Windows guide](duckdb_from_command_line_on_windows.md) |

Each guide includes installation, verification, SQL practice, and recovery
steps. **Use the Markdown guides for this revision.** The existing PDFs
have not been updated and may contain older instructions.

Download or clone the **whole folder**, then extract any zip. Keep:

```text
DuckDB_from_Command_Line/
  README.md
  duckdb_from_command_line_on_macbook.md
  duckdb_from_command_line_on_windows.md
  data/
    students.csv
```

[students.csv](data/students.csv) has **8 data rows plus a header**.
You will create `report.sql` during Section 5. The optional startup
diagnostic in Section 6 explains how to create `clean_start.sql`. Neither
SQL file is supplied in this folder.

## A Simple Route Through the Lesson

1. Open the guide for **your computer only**. Do not follow both guides.
2. Try `duckdb --version`. If it works, skip installation.
3. Use **one** installation method if needed; do not install several copies.
4. Open the tutorial folder and check that the CSV query returns **8**.
5. Follow the SQL practice in your guide.

**Sections 3 and 6 below are help pages. Skip them when things work.**
You do not need to read every possible error before starting.

**A few words:** a *terminal* is the window where you type commands; a
*shell* reads those commands; *CLI* means command-line interface; a *path*
is a file location. **PATH** is the list of folders searched for programs.
**Enter** and **Return** mean the same key here.

## 1. Know Which Prompt You Are Using

| Prompt/location | Enter here |
|---|---|
| macOS Terminal shell (often ends in `%` or `$`) | `duckdb`, `cd`, installation commands |
| Windows PowerShell (`PS ...>`) or Command Prompt (`C:\...>`) | `duckdb`, folder commands, installation commands |
| DuckDB (`D`) | SQL ending in `;`, or dot-commands such as `.quit` |
| Python (`>>>`) | You are in the wrong program for this lesson; enter `exit()` |

Do not type the displayed prompt symbols. Enter one command or code block
at a time. If at `D`, enter `.quit` before running terminal commands. If
input is unfinished, press Ctrl+C first to cancel it. A continuation prompt
can mean a missing semicolon, unmatched quote, or unmatched parenthesis.

Windows Terminal hosts different shells: check the tab's shell name. Follow
these Windows instructions in **PowerShell or Command Prompt**, not WSL or
Git Bash. Do not double-click the executable to follow this lesson: launch
it from a terminal opened in the tutorial folder.

## 2. First Check: Can DuckDB Run?

**In your terminal shell**, run:

```text
duckdb --version
duckdb -c "SELECT 6 * 7 AS answer;"
```

Run these separately. Expect a version and **42**. If they work, go to
Section 4. `import duckdb` working in a notebook does not establish that
the terminal can find the standalone DuckDB program.

If you see **command not found**, **not recognized**, or **The term
'duckdb' is not recognized**, follow Section 3. PATH is just the list of
folders searched for an executable when you type its short name.

## 3. Fix Installation or PATH

### Mac: Install or Locate DuckDB (skip on Windows)

If you already have Homebrew:

```bash
brew --version
brew install duckdb
```

If installation succeeds and `duckdb --version` works, go to Section 4.
If `brew` is unavailable, use the manual route below; you do not need to
install Homebrew just for this lesson. Existing Homebrew users can consult
[its setup instructions](https://docs.brew.sh/Installation) if needed.

**Manual route, without administrator access:**

1. Open [DuckDB's installation page](https://duckdb.org/install/), select
   macOS, CLI, current stable, and download `duckdb_cli-osx-universal.zip`.
2. Unzip it in Finder. Find the actual `duckdb` executable.
3. Open your Home folder (Shift+Cmd+H), create `duckdb-cli`, and move the
   executable there. Do not leave it inside an extra extraction subfolder.
4. Run in Terminal:

```bash
ls -l "$HOME/duckdb-cli/duckdb"
chmod +x "$HOME/duckdb-cli/duckdb"
"$HOME/duckdb-cli/duckdb" --version
```

If the first command fails, fix the file location before continuing.
If the last command succeeds, add the containing folder for this session:

```bash
export PATH="$HOME/duckdb-cli:$PATH"
duckdb --version
```

To keep that setting for future Terminal sessions (the normal macOS
**zsh** shell), copy and run this whole line once:

```bash
printf '\nexport PATH="$HOME/duckdb-cli:$PATH"\n' >> "$HOME/.zshrc"
```

`$HOME` means your home folder: copy it exactly, without substituting your
name. The command adds the setting to a file that Terminal reads when it
starts. Open a new Terminal window and run `duckdb --version` again.
If you use a different shell, ask the instructor or use the full path.

**Only if an earlier installation is still not found:** try the location
that matches your installation. These are alternative checks, not commands
to install three copies:

```bash
/opt/homebrew/bin/duckdb --version
/usr/local/bin/duckdb --version
"$HOME/.duckdb/cli/latest/duckdb" --version
```

The first two are common Homebrew locations; the third is used by DuckDB's
installer script. For working Homebrew outside PATH, use the appropriate
one of these commands:

```bash
# Apple Silicon Homebrew:
eval "$(/opt/homebrew/bin/brew shellenv)"
# Intel Homebrew alternative:
eval "$(/usr/local/bin/brew shellenv)"
```

Then run `brew list duckdb`; if absent, run `brew install duckdb`. Follow
Homebrew's startup-file instructions for a persistent PATH fix. To inspect
command resolution, use `command -v duckdb` and `type -a duckdb`. An alias
or older installation may be taking precedence.

For a trusted manual download blocked by Gatekeeper, follow [Apple's
Privacy & Security instructions](https://support.apple.com/en-us/102445).
If permission, malware, or device-policy warnings remain, ask the instructor
or IT. Do not disable system security. A wrong-platform binary or unsupported
OS is not a PATH problem; select the correct CLI and check compatibility.

### Windows: Install or Locate DuckDB (skip on Mac)

For beginners, open **Command Prompt** from Start (type `cmd`). These
two installation commands also work in PowerShell:

```text
winget --version
winget install --id DuckDB.cli --exact
```

If WinGet is unavailable, install/update Microsoft's **App Installer** if
permitted, or use the manual route. If installation fails, resolve that
error first. Close and reopen the entire terminal application after success.
WinGet availability and device policy vary; see [Microsoft's WinGet guide](https://learn.microsoft.com/en-us/windows/package-manager/winget/).

**Manual route, in your own user folder:**

1. On [DuckDB's installation page](https://duckdb.org/install/), select Windows,
   CLI, current stable. In Windows Settings > System > About, check System
   type: use `amd64` for x64 Intel/AMD, or `arm64` for Arm.
2. Download the matching zip and choose **Extract All**.
3. In File Explorer's address bar enter `%USERPROFILE%`. Create `duckdb-cli`
   there and move the actual `duckdb.exe` into it. Enable **File name
   extensions** to inspect the filename. Do not run inside the zip.
4. Test it using the appropriate shell:

**PowerShell:**

```powershell
Test-Path "$env:USERPROFILE\duckdb-cli\duckdb.exe"
& "$env:USERPROFILE\duckdb-cli\duckdb.exe" --version
```

**Command Prompt:**

```bat
dir "%USERPROFILE%\duckdb-cli\duckdb.exe"
"%USERPROFILE%\duckdb-cli\duckdb.exe" --version
```

If the file is missing, correct its location first. PowerShell requires `&`
to execute a quoted path. If you are already inside the executable's folder,
PowerShell needs `.\duckdb.exe`, not just `duckdb.exe`.

**If full-path execution works, repair name lookup:**

- Search Start for **Edit environment variables for your account**.
- Under User variables, edit **Path** (create it if absent).
- Add the full folder path copied from File Explorer, without quotes and
  without `duckdb.exe`. Preserve the existing entries.
- Restart the whole terminal application; also restart VS Code if using
  its terminal. New tabs can inherit the parent's older environment.
- Test `where.exe duckdb` and `duckdb --version`.

For this session only, you can instead add the folder as follows:

```powershell
# PowerShell
$env:Path = "$env:USERPROFILE\duckdb-cli;$env:Path"
```

```bat
REM Command Prompt
set "PATH=%USERPROFILE%\duckdb-cli;%PATH%"
```

`%USERPROFILE%` (Command Prompt) and `$env:USERPROFILE` (PowerShell)
mean your home folder. Copy those expressions exactly as shown.

These paths describe the manual route above; substitute the real folder
if you installed elsewhere. For a WinGet install, inspect
`winget list --id DuckDB.cli --exact`. If it reports an installation but
lookup still fails after restarting, ask the instructor to inspect its
executable/link location, or use the permitted manual route.

In PowerShell, `Get-Command duckdb -All` can show aliases or multiple copies.
Bare `where` is an alias for a different command; use **where.exe**.
See [PowerShell command resolution](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_command_precedence).

**File exists but launch fails:**

- Missing `VCRUNTIME`/`MSVCP` DLL: install/repair the matching
  [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist).
- “This app cannot run on your PC”: verify architecture, OS compatibility,
  and that you extracted the Windows executable rather than a library.
- SmartScreen: verify the official source; use “More info > Run anyway”
  only if offered and allowed by policy. Otherwise ask IT.
- A file disappears or execution is blocked: inspect security notifications
  and ask IT. WinGet is not an exemption from security policy.

### If PATH Still Fails: Use the Program File Directly

You do not have to finish fixing PATH before learning SQL. Replace the
initial `duckdb` in a terminal command with the verified launcher:

```bash
# Mac manual installation
"$HOME/duckdb-cli/duckdb" -c "SELECT 42;"
```

```powershell
# Windows PowerShell manual installation
& "$env:USERPROFILE\duckdb-cli\duckdb.exe" -c "SELECT 42;"
```

```bat
REM Windows Command Prompt manual installation
"%USERPROFILE%\duckdb-cli\duckdb.exe" -c "SELECT 42;"
```

Using the program file's full location avoids a PATH problem. It cannot
fix a blocked program, a missing Windows component, or an unsupported OS.

## 4. Second Check: Find the Tutorial Data

**Mac:** in Terminal type `cd ` (with the trailing space), drag this tutorial
folder from Finder into Terminal, and press Return. Then:

```bash
pwd
ls data/students.csv
```

**Windows:** open the tutorial folder in File Explorer, type `cmd` in the
address bar, and press Enter. In that Command Prompt:

```bat
cd
dir data\students.csv
```

**PowerShell alternative:** use `Set-Location` followed by the actual full
folder path in quotes, then `Get-Location` and `dir data\students.csv`.
Use “Copy as path” in File Explorer; do not assume Desktop is outside OneDrive.

To navigate manually in CMD across drives, use `cd /d "actual folder path"`.
In PowerShell use `Set-Location "actual folder path"`; `/d` is CMD-specific.
Bare `cd` displays the folder in CMD but changes to home in PowerShell.
On Mac, quote a home-relative path with `$HOME`, for example
`cd "$HOME/Desktop/OMIS 105 Labs"`; quoted `"~/..."` does not expand `~`.

From the correct folder, run:

```text
duckdb -c "SELECT COUNT(*) AS students FROM read_csv('data/students.csv');"
```

Expect **8**. If the 42 check works but this fails, focus on folder, filename,
file content, and read permissions. Check that synced files are downloaded
locally. The CSV should begin `id,name,major,gpa`, not HTML.

## 5. Query, Save, and Run Scripts

In the terminal, type `duckdb` and press Enter. When you see `D`, copy
the following SQL and press Enter after the final semicolon:

```sql
SELECT major, ROUND(AVG(gpa), 2) AS avg_gpa
FROM read_csv('data/students.csv')
GROUP BY major
ORDER BY avg_gpa DESC, major;
```

Expected values:

| Major | Average GPA |
|---|---:|
| Information Systems | 3.83 |
| Accounting | 3.50 |
| Finance | 3.35 |
| Marketing | 3.35 |

`3.5` and `3.50` are the same numeric result. Border style, column types,
colors, and elapsed times can vary. Use `.mode table` for plain ASCII borders,
or `.mode duckbox` and `.headers on` to restore the usual display.

Create **report.sql** in this tutorial folder using a plain-text editor.
Use VS Code, Notepad with **All files** selected, or TextEdit in plain-text
mode; check that the name is not `report.sql.txt`. Save:

```sql
SELECT COUNT(*) AS students FROM read_csv('data/students.csv');
SELECT major, ROUND(AVG(gpa), 2) AS avg_gpa
FROM read_csv('data/students.csv')
GROUP BY major
ORDER BY avg_gpa DESC, major;
```

Exit DuckDB with `.quit`. In the terminal, run your saved script:

```text
duckdb -bail -f report.sql
```

Or, if already inside DuckDB, enter `.read report.sql` on a fresh line.
The script does not change the CSV or create tables. Relative paths inside
it resolve from the process's working directory, **not** automatically from
the SQL file's own directory. For script paths with spaces, the shell command
`duckdb -bail -f "my reports/report.sql"` avoids nested dot-command quoting.

For persistent tables, start `duckdb class_cli.db` from the tutorial folder.
At D, run this once:

```sql
CREATE TABLE students AS
SELECT * FROM read_csv('data/students.csv');
```

Exit and reopen the same database, then query `SELECT COUNT(*) FROM students;`.
Expect 8. If the table already exists, query it rather than recreating it.
Use `.databases` and `.tables` to check where you are. Parent folders must
exist and be writable. `.open` switches databases; it does not save your
in-memory tables into a file. The statements in this lesson save automatically. If your instructor
has you start a transaction with `BEGIN`, finish it with `COMMIT`.

## 6. Other Common Errors

| Symptom | What to check |
|---|---|
| SQL typed in the shell says “command not found” | Run `duckdb` first; enter SQL only at D. |
| `duckdb` or `cd` typed at D fails | Ctrl+C to clear unfinished input, then `.quit`; use the shell. |
| CLI waits after a statement | Add the missing semicolon, or Ctrl+C and retype if quotes/parentheses are unmatched. |
| `.tables;` fails | Dot-commands have no semicolon and must be on their own line. |
| `students` does not exist | Reading the CSV directly does not create a stored table; you may also have reopened the wrong database. |
| Database seems empty | Check the current folder, `.databases`, and whether the earlier session was in-memory. |
| Cannot set lock | Close other CLI sessions and notebook connections to the same database. Do not delete `.wal` files to force it open. |
| Read-only / cannot write / cannot open | Check parent-folder existence, permissions, `-readonly`, disk space, and sync status. Prefer a local user-owned folder. |
| File-version incompatibility | Preserve the database and ask the instructor about the DuckDB version that created it; do not overwrite it. |
| Script saved but not found | Check for `.sql.txt`, wrong folder, or rich-text format. Use plain text and show filename extensions. |
| Quoting error after copying | Use straight quotes and normal hyphens; copy from Markdown, without prompt labels. |
| Garbled output borders | Try `.mode table`; do not confuse it with `.mode ascii`. |
| Unexpected startup commands/settings | Run the clean-start check below; do not delete personal configuration. |

**Optional: only if DuckDB runs unexpected commands when it starts.**
A file named `.duckdbrc` can store personal settings. To ignore it for one
run, first create a
plain-text file named **clean_start.sql** in this folder containing only:

```sql
-- No startup settings
```

Then, from this folder, run:

```text
duckdb -init clean_start.sql -c "SELECT 42 AS answer;"
```

For complex SQL containing `$`, `!`, or nested quotes, put it in a plain-text
`.sql` file and use `-f`. Shell expansion differs from SQL quoting.

If still stuck, send the instructor your OS, shell, exact command, full error,
whether full-path `--version` works, current folder, and whether the sample
files exist. Redact private directory names before sharing. If downloads fail
because of network, certificate, or proxy policy, ask IT; do not disable TLS
verification. An unsupported OS or locked-down device may need another
instructor-approved machine.

## Validation and Official References

These guides were checked against current documentation. On DuckDB 1.5.5 on macOS, checks passed for the 42 query, eight-row CSV
count, GPA values and ordering, `-f`/`.read`, table/schema inspection, CSV
output, persistence across processes, paths with spaces, and full-path
launch without the executable folder in PATH. This revision updates Markdown only; the existing PDF handouts are not
synchronized with these instructions. Windows
installation and security dialogs require a Windows machine to validate.
No guide can guarantee operation on every managed device or OS version.

- [DuckDB installation and platform downloads](https://duckdb.org/install/)
- [DuckDB CLI overview](https://duckdb.org/docs/current/clients/cli/overview)
- [CLI arguments](https://duckdb.org/docs/current/clients/cli/arguments)
- [Dot-commands](https://duckdb.org/docs/current/clients/cli/dot_commands)
- [Output formats](https://duckdb.org/docs/current/clients/cli/output_formats)
- [Homebrew installation](https://docs.brew.sh/Installation)
- [Microsoft WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
- [Apple application security](https://support.apple.com/en-us/102445)
