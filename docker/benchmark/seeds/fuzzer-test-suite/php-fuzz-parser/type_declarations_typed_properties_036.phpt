<?php
$foo = new class {
    public int $bar = 10, $qux;
};

foreach ($foo as $key => $bar) {
    var_dump($key, $bar);
}
?>