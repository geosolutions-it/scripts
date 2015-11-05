#!/usr/bin/perl 
# AJPING - pings a servlet engine with AJP protocol
# Sends:   \x12\x34\x00\x01\x0a
# Expects: \0x41\0x42\0x00\0x01\0x09 
# 
use strict;
use Socket;             # Part of perl
use Time::HiRes 'time'; # http://search.cpan.org/~jhi/Time-HiRes-1.9721/HiRes.pm

sub xdie;
sub usage;

my ($host, $port);

if (@ARGV == 2) {
  $host = $ARGV[0];
  $port = $ARGV[1];  
} else {
  ($host, $port) = split (/:/, shift @ARGV, 2);
}

if (!$host || !$port) {
  usage();
}

for (my $i = 0; $i < 10; $i++) {
  my $start = time();
  my $iaddr = inet_aton($host) || xdie("Unknown host ($host)");
  my $paddr = sockaddr_in($port, $iaddr) || xdie ("Unable to establish a socket address");
  my $proto = getprotobyname('tcp');
  socket(my $sock, PF_INET, SOCK_STREAM, $proto) || xdie "Unable to create a socket.";
  connect($sock, $paddr)  || xdie "Unable to connect to server";
  syswrite $sock, "\x12\x34\x00\x01\x0a";
  sysread $sock, my $recv, 5 || die "read: $!, stopped";
  my @vals = unpack 'C5', $recv;
  my @acks = qw (65 66 0 1 9);
  my %vals = map {$_, 1} @vals;
  my @diff = grep {!$vals {$_}} @acks;

  if (@diff == 0) {
    printf "Reply from $host: %d bytes in %3.3f seconds\n", (length("@vals") - $#vals), (time() - $start);  
  } else {
    print "Protocol error: unable to verify AJP host $host:$port\n";
    exit 1;
  }
  close($sock);
  sleep(1);
}

exit;

sub usage {
  print "ajping - pings a server via AJP protocol\n";
  print "usage: ajping host:port\n";
  print "       ajping host port\n";
  exit;
}

sub xdie {
  my $msg = shift;
  printf STDERR "ERROR: $msg\n";
  exit 1;
}
