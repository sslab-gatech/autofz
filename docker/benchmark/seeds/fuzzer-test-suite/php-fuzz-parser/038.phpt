<?php

try {
    var_dump(array(function() { } => 1));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>