<?php

function &gen($items) {
    foreach ($items as $key => &$value) {
        yield $key => $value;
    }
}

var_dump(...gen(['a', 'b', 'c']));

?>