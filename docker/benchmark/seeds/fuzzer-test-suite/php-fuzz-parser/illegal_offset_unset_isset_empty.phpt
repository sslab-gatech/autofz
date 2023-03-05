<?php

$ary = [];
try {
    unset($ary[[]]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    isset($ary[[]]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    empty($ary[[]]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>