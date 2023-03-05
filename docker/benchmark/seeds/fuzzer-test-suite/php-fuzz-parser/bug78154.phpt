<?php

namespace {
    try {
        var_dump(similar_text('a', 'a', $c=0x44444444));
        var_dump($c);
    } catch (Throwable $e) {
        echo "Exception: " . $e->getMessage() . "\n";
    }
}
namespace Foo {
    try {
        var_dump(similar_text('a', 'a', $d=0x44444444));
        var_dump($d);
    } catch (\Throwable $e) {
        echo "Exception: " . $e->getMessage() . "\n";
    }
}

?>