<?php
$varName = 'var';
$propName = 'prop';
try {
    $$varName->$propName =& $$varName;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($var);
?>