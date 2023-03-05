<?php

var_dump(get_included_files());

include(__DIR__."/014.inc");
var_dump(get_included_files());

include_once(__DIR__."/014.inc");
var_dump(get_included_files());

include(__DIR__."/014.inc");
var_dump(get_included_files());

echo "Done\n";
?>