<?php
spl_autoload_register(function ($class) {
  $GLOBALS['include'][] = $class;
  eval("class DefClass{}");
});

$a = new DefClass;
print_r($a);
print_r($GLOBALS['include']);
?>