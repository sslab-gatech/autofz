<?php
try {
    $u1->a += 5;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    $x = ++$u2->a;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    $x = $u3->a++;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    $u4->a->a += 5;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>