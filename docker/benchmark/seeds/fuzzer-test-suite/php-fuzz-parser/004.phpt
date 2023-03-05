<?php

var_dump(strncmp("", "", 100));
try {
    var_dump(strncmp("aef", "dfsgbdf", -1));
} catch (\ValueError $e) {
    echo $e->getMessage() . \PHP_EOL;
}
var_dump(strncmp("fghjkl", "qwer", 0));
var_dump(strncmp("qwerty", "qwerty123", 6));
var_dump(strncmp("qwerty", "qwerty123", 7));

?>