<?php
$s = "hello";
$a = true;

echo "--> read access:";
echo $a->p;

echo "\n--> direct assignment:\n";
try {
    $a->p = $s;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "\n--> increment:\n";
try {
    $a->p++;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "\n--> reference assignment:\n";
try {
    $a->p =& $s;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "\n--> reference assignment:\n";
try {
    $s =& $a->p;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "\n--> indexed assignment:\n";
try {
    $a->p[0] = $s;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "\n--> Confirm assignments have had no impact:\n";
var_dump($a);
?>