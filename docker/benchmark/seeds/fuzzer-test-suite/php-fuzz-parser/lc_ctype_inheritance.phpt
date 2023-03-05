<?php

var_dump(setlocale(LC_CTYPE, "0"));
var_dump(bin2hex(strtoupper("\xe4")));
var_dump(preg_match('/\w/', "\xe4"));
var_dump(setlocale(LC_CTYPE, "de_DE", "de-DE") !== false);
var_dump(bin2hex(strtoupper("\xe4")));
var_dump(preg_match('/\w/', "\xe4"));
?>