<?php

function gen() { yield; }

$gen = gen();

try {
    count($gen);
} catch (Exception $e) {
    echo $e;
}

?>