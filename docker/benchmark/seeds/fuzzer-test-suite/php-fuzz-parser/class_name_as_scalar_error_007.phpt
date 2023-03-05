<?php

try {
    var_dump(self::class);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump([self::class]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>