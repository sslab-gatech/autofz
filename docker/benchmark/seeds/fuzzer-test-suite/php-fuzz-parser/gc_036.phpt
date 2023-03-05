<?php
function &foo() {
    $a = [];
    $a[] =& $a;
    return $a;
}
function bar() {
    gc_collect_cycles();
}
bar(foo());
echo "ok\n";
?>