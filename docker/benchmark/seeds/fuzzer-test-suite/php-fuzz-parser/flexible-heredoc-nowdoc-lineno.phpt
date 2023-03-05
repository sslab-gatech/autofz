<?php

$heredoc = <<<EOT
hello world
EOT;

$heredoc = <<<'EOT'
hello world
EOT;

$heredoc = <<<EOT
 hello world
 EOT;

$heredoc = <<<'EOT'
 hello world
 EOT;

try {
	throw new exception();
} catch (Exception $e) {
	var_dump($e->getLine());
}

?>