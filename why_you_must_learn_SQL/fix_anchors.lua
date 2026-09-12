-- Pandoc Lua filter: make the .md's existing <a id="section-N"></a> anchors
-- work in the LaTeX/PDF output too.
--
-- The .md deliberately uses raw HTML anchors (not pandoc's {#id} heading
-- attribute syntax) so the file still renders correctly as plain Markdown
-- on GitHub. That's the right call for the source file — but pandoc's
-- LaTeX writer silently drops raw HTML blocks it can't use, so the manual
-- "## Table of Contents" section's links (#section-1, #section-2, ...)
-- had no matching \label in the PDF and came up as broken references.
--
-- This filter only runs for LaTeX output: wherever it finds
-- <a id="X"></a>, it substitutes a \hypertarget{X}{}\label{X} at that same
-- spot, which is what pandoc would have generated had the anchor been a
-- real heading identifier. The .md source itself is untouched.

local function latex_target(id)
  return "\\hypertarget{" .. id .. "}{}\\label{" .. id .. "}"
end

-- pandoc parses a standalone <a id="x"></a> as a RawBlock when it forms a
-- whole HTML block by itself, but as a RawInline (inside a Para) when it's
-- short enough to read as inline HTML. Handle both.

function RawBlock(el)
  if FORMAT == "latex" and el.format == "html" then
    local id = el.text:match('<a%s+id="([^"]+)"')
    if id then
      return pandoc.RawBlock("latex", latex_target(id))
    end
  end
end

function RawInline(el)
  if FORMAT == "latex" and el.format == "html" then
    local id = el.text:match('<a%s+id="([^"]+)"')
    if id then
      return pandoc.RawInline("latex", latex_target(id))
    end
  end
end
