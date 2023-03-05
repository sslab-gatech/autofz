<?php

function test_slice1() {
    var_dump(array_slice(func_get_args(), 1));
}
function test_slice5() {
    var_dump(array_slice(func_get_args(), 5));
}

test_slice1(1, 2, 3);
test_slice5(1, 2, 3);

?>