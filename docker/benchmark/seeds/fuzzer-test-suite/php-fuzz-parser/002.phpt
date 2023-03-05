<?php

function test1() {
    try {
        var_dump(func_get_arg(-10));
    } catch (\ValueError $e) {
        echo $e->getMessage() . \PHP_EOL;
    }

    try {
        var_dump(func_get_arg(0));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
    try {
        var_dump(func_get_arg(1));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
}

function test2($a) {
    try {
        var_dump(func_get_arg(0));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
    try {
        var_dump(func_get_arg(1));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
}

function test3($a, $b) {
    try {
        var_dump(func_get_arg(0));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
    try {
        var_dump(func_get_arg(1));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
    try {
        var_dump(func_get_arg(2));
    } catch (\Error $e) {
        echo $e->getMessage() . \PHP_EOL;
    }
}

test1();
test1(10);
test2(1);
try {
    test2();
} catch (Throwable $e) {
    echo "Exception: " . $e->getMessage() . "\n";
}
test3(1,2);

call_user_func("test1");
try {
    call_user_func("test3", 1);
} catch (Throwable $e) {
    echo "Exception: " . $e->getMessage() . "\n";
}
call_user_func("test3", 1, 2);

class test {
    static function test1($a) {
        try {
            var_dump(func_get_arg(0));
        } catch (\Error $e) {
            echo $e->getMessage() . \PHP_EOL;
        }
        try {
            var_dump(func_get_arg(1));
        } catch (\Error $e) {
            echo $e->getMessage() . \PHP_EOL;
        }
    }
}

test::test1(1);
try {
    var_dump(func_get_arg(1));
} catch (\Error $e) {
    echo $e->getMessage() . \PHP_EOL;
}

echo "Done\n";
?>