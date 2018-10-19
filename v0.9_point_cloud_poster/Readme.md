First - download and install MiKTeX (https://miktex.org/) and then get a TeX editor. I use TeXStudio (https://www.texstudio.org/). Download this entire folder and put it wherever you like. Open the .tex file in TexStudio and click Build and View (overlapping play buttons - F5). It will probably ask to install some things the first time you click build+view, just keep saying yes.

Template poster file with logos. Boxes in each column should size dynamically to fit each other with the text (unless you over spill the entire length).

If you want to change the width of the columns, edit the span parameter, currently defined in the headerbox for Procedure Overview as 2.

One is the base value, and it makes the column take on that multiple of width. Do this for all the boxes in a column if you decide to change.

You can go to column=2 in the headerbox if you like for a third column. It should be self-explanatory looking at the TeX code.


%%Just open a terminal on makefile level and type "make".
