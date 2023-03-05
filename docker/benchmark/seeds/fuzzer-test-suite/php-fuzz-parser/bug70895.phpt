<?php

try {
    array_map("%n", 0);
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    array_map("%n %i", 0);
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    array_map("%n %i aoeu %f aoeu %p", 0);
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
?>