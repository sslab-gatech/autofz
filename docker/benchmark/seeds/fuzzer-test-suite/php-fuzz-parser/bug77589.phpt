<?php
var_dump(
    parse_ini_string(<<<INI
[0]
a = 1
b = on
c = true

["true"]
a = 100
b = null
c = yes
INI
, TRUE, INI_SCANNER_TYPED));

?>