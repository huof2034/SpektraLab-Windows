spektralab-host is free software under the GNU General Public License,
version 3 or (at your option) any later version (SpektraLab-GPL-3.0.txt).
The full corresponding source is the SpektraLab repository at the commit
this build was made from.

Bundled third-party components:
  LibRaw 0.22.2        LGPL-2.1, statically linked; source: libraw.org, and
                       engine/setup-libraw.sh fetches the exact pinned tree.
  stb_image, stb_image_write, stb_truetype   public domain / MIT (stb-LICENSE.txt)
  volk                 MIT (volk-LICENSE.txt)
  Vulkan-Headers       Apache-2.0 OR MIT, compile time only
  libjpeg-turbo 3.2.0   IJG and BSD-3-Clause, statically linked
  libpng 1.6.59        PNG Reference Library License v2, statically linked
  zlib-ng 2.3.3        zlib license, statically linked
  libheif 1.23.6      LGPL-3.0, statically linked, HEVC input only
  libde265 1.1.3      LGPL-3.0, statically linked
  OpenEXR 3.5.2      BSD-3-Clause, statically linked (plus embedded
                      libdeflate MIT, OpenJPH BSD-2-Clause, zstd BSD-3-Clause)
  Imath 3.2.3        BSD-3-Clause, statically linked
  LittleCMS 2.19.1   MIT, statically linked
  Lensfun 0.3.99    LGPL-3.0, static; bundled calibration database CC BY-SA 3.0
  GLib 2.86.5      LGPL-2.1-or-later, static; libffi, PCRE2, proxy-libintl
                    notices and source pins included in licenses/.
Exact codec sources and checksums: engine/setup-codecs.sh / setup-codecs.ps1.
Input codec sources/checksums: engine/cmake/input-codecs-pins.json;
engine/setup-input-codecs.py builds them without fetching unpinned subprojects.
This software is based in part on the work of the Independent JPEG Group.
The original spektrafilm profiles and print LUTs under engine/: CC BY-SA 4.0
(Profiles-and-LUTs-CC-BY-SA-4.0.txt, with attribution in the CHANGELOG).
SpektraLab's black-and-white product profiles: Product-profiles-NOTICE.md.
Embedded Liberation Sans imprint fonts: Imprint-fonts-LICENSE.txt (SIL OFL 1.1).
stb_truetype: stb-LICENSE.txt (MIT option).
