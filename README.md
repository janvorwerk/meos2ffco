# meos2ffco
Export of the results from MeOS orienteering software for the French FFCO ("Classement National").

# Principle
MeOS has one single field for first name and surname,
therefore we lookup the FFCO archive to retrieve the proper fields
so that "Jean DU PONT" does not split up as "Jean DU" / "PONT"

# How to run?
To run this program you need Python 3.x installed.
Then you open the command line and provide:
 - the path of the FFCO archive
 - the path of the MeOS CSV export file
 - the output path of the resulting file

```
$ ./meos2ffco.py licencesFFCO-2016-au-04-10-2016.csv export_MD.csv out.csv
```

# Races with variations
If the race has got variations on the circuit (mass start), you will want to use the
MeOS category (which typically matches the gross circuit w/o the variations) as the circuit
name (which in MeOS is the circuit including the variations).
To do so, edit main.py and set `USE_CAT_AS_CIRCUIT = False`

# Caveats
The command line is a pain to type... editing the file as you're told above is even worse...
ideally, it should be a GUI application...
