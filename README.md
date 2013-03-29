Description
---

This project was realized during the MAKE Finance 22.-23. March 2013 in Berne and Sierre.  
Further information about the project is available [here](http://make.opendata.ch/wiki/project:finanzausgleich_bern).

Take a look at the [visualization](http://wag.github.com/finanzausgleich-bern/web)!

Developers
---

Fetch the sources, then build the submodule.

    git submodule init
    git submodule update


Possible improvements
---

 * Include the municipalities of the sections, one section at a time, f.e. clicking a section opens
   the money strains from the selected section to the newly added municipalities. A part of this has been realized, see the 'municipalities' branch.
 * Add a scale from 0 to ~ 1 Bil. to visualize the sizes without requiring to hover over.
 * Flip tooltip if it hits bottom.
 * Automatically redraw the svg if the window gets resized.
