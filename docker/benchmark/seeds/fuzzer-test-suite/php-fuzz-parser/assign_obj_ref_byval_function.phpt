<?php

function notRef() {
    return null;
}

$obj = new stdClass;
$obj->prop =& notRef();
var_dump($obj);

?>