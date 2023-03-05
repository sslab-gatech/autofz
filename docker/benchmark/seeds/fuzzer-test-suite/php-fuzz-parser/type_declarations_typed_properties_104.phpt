<?php
declare(strict_types=1);
$o = new class {
    public string $a = "123";
};
$x = & $o->a;
try {
    $ret = ++$x + 5;
} catch (TypeError $e) {
}
?>
OK