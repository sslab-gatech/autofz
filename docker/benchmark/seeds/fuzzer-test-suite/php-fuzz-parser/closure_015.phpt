<?php

$x = function() { return 1; };
try {
    print (string) $x;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    print $x;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>