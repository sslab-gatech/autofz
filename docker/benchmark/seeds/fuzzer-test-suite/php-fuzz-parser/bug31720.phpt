<?php
$array = array('at least one element');

try {
    array_walk($array, array($nonesuchvar,'show'));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
?>