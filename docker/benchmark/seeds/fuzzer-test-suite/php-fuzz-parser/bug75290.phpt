<?php

var_dump((new ReflectionFunction('sin'))->getClosure());

var_dump(function ($someThing) {});

?>