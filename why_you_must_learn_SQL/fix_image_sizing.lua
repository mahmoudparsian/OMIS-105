-- Pandoc Lua filter: size images for the LaTeX/PDF output only.
--
-- The .md uses plain ![alt](path) image syntax on purpose, with no
-- pandoc {width=...} attribute — that attribute syntax isn't part of
-- standard Markdown, so GitHub would print it as literal text right next
-- to the image instead of consuming it. Setting the width here, in the
-- build pipeline, keeps the .md source portable while still giving the
-- PDF a sensibly-sized figure instead of the image's native pixel size
-- (which is usually much wider than the page's text block).

function Image(img)
  if FORMAT == "latex" and not img.attributes.width then
    img.attributes.width = "6in"
  end
  return img
end
