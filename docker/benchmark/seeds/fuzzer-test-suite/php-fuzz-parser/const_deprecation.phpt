<?php

var_dump(ZEND_TEST_DEPRECATED);
var_dump(constant('ZEND_TEST_DEPRECATED'));

const X = ZEND_TEST_DEPRECATED;
var_dump(X);

?>