<?php

try {
    func_get_args();
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}

?>