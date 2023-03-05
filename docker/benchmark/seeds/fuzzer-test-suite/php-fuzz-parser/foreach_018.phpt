<?php

$obj = (object)[
    "\0A\0b" => 42,
    "\0*\0c" => 24,
];

foreach ($obj as $k => $v) {
    var_dump($k, $v);
}

?>