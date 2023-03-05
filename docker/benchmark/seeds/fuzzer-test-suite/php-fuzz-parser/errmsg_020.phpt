<?php

try {
    phpinfo();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>