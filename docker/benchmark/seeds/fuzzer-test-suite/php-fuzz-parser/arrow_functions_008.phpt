<?php

// This doesn't make terribly much sense, but it works...

$fn = fn() => yield 123;
foreach ($fn() as $val) {
    var_dump($val);
}

$fn = fn() => yield from [456, 789];
foreach ($fn() as $val) {
    var_dump($val);
}

$fn = fn() => fn() => yield 987;
foreach ($fn()() as $val) {
    var_dump($val);
}

?>