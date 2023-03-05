<?php

interface I {}
require __DIR__ . '/bug77652.inc';
$data = require __DIR__ . '/bug77652.inc';
print_r(class_implements($data['I']()));

?>