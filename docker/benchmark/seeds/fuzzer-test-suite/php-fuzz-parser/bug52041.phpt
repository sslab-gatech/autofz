<?php
function foo() {
    return $x;
}

try {
    foo()->a = 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    foo()->a->b = 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    foo()->a++;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    foo()->a->b++;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    foo()->a += 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    foo()->a->b += 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

foo()[0] = 1;
foo()[0][0] = 2;
foo()[0]++;
foo()[0][0]++;
foo()[0] += 2;
foo()[0][0] += 2;

var_dump(foo());
?>