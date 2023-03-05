<?php
$a = [function () { echo "123\n"; }, '__invoke'];
$a();

$b = Closure::fromCallable($a);
$b();
?>