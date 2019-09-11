## Self-Documenting (attempts) at Automating Directory Updates

really for my own future reference : )
### Editing images
for when given a folder of images. 
When it's in a big folder and I want to use command line stuff, this means that it's a new semester and there's should be a box folder of photos with filenames like 190000_Comp Bio_LAST_FIRST_69.jpg
The directory html mostly uses the format Last_First.jpg so I use regex to remove/rename parts of the filename.

    rename -v -f 's/(\d+_Comp Bio_)([A-_]+)(_\d+)/$2/' *.jpg
asdf

	    rename -v 's/.+_.+/\L$&/' *.jpg
	    rename -v 's/^[a-z]/\U$&/' *.jpg
	    rename -v 's/_[a-z]/\U$&/' *.jpg
for proper capitalization.

temp
rename -v 's/^(190820_Comp Bio_)|(_\d+)//' *.jpg

what i'm trying to achieve with the regex is selecting and removing the text that isn't the name...

ls | grep -P "remove.+.jpg" | xargs -d"\n" rm
