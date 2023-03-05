<?php

class Test {
    public function __destruct() {}
}

$test = new Test;
$test->foo = [&$test->foo];
$ary = [&$ary, $test];
unset($ary, $test);
gc_collect_cycles();

?>
===DONE===