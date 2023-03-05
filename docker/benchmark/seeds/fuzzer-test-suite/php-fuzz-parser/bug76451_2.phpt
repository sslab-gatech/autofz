<?php
class Foo {}
class_alias('Foo', 'Bar');

require __DIR__ . '/bug76451_2.inc';
?>
===DONE===