This documentation is created by Tashrif Billah for referring AMP-SCZ collaborators about how to make an NDA-format dictionary definition. The latter has to be sent to ndahelp@mail.nih.gov to create the actual data dictionary. Copy the [](nda_data_structure_template.csv) and start editing it according to the following instructions:


#### ElementName:
      Must be less than 30 characters. It could be identical to REDCap variable name. If a REDCap variable does not exist, make up a proper name.


#### DataType:
  * String
  * Date
  * Integer
  * Float


#### Size:
      It is valid only for String `DataType`. It is okay to provide an overestimate for the number of characters.


#### Required:
      Unless required, keep this as `Recommended` whenever possible.


#### ElementDescription:
      Put a one liner describing the `ElementName`


#### ValueRange:
      It is the most important field. An underestimate will result in data submission error. If your value range is mathematically established, put exact numbers such as `0::100`. If it is not mathematically established, put overestimates on both lower and upper limits. If you are not comfortable putting a range, keep it empty. Include `-300, -900` for Integer and Float types e.g. `0::100; -300; -900`. Multiple ranges, separated by semicolon, can be written in one cell.


#### Notes:
      If necessary, put any additional note beside `ElementDescription`. Keep empty otherwise.


#### Aliases:
      Keep it empty. NDA database team will populate this cell if necessary.


---

#### Pro tip:
(i) No need to enclose a string with double quotes unless you have space, comma, or semicolon in that string.
