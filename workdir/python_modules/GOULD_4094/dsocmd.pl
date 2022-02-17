#!/usr/bin/perl
use strict;
use warnings;
use Device::SerialPort;
use Time::HiRes;
use Getopt::Long;
use POSIX qw/strftime/;

# plot destination
# check for tools




# defaults
my $baudrate=9600;
my $port;


my $opt_command;
my $opt_help;
my $opt_macro;
my $opt_plot;
my $opt_capture;
my $opt_quiet;
my $opt_show;
my $opt_pdf;
my $ser_dev = "/dev/ttyUSB0";



GetOptions ('h|help'      => \$opt_help,
              'c|cmd=s'   => \$opt_command,
              'tty=s'     => \$ser_dev,
              'baud=s'    => \$baudrate,
              'capture=s' => \$opt_capture,
              'm|macro=s' => \$opt_macro,
              'plot'      => \$opt_plot,
              'q|quiet'   => \$opt_quiet,
              'show'      => \$opt_show,
              'pdf'       => \$opt_pdf
            );
           
# define VERBOSE file handle to print debug output
if ($opt_quiet) {
   open(VERBOSE, '>', "/dev/null") or die;
} else {
   *VERBOSE = *STDOUT;
}
           
# you entered help option, let's print the help screen and quit
if($opt_help) {
    help();
    exit(0);
}



if(defined($opt_command)){
  init_port();
  communicate($opt_command);
  #print "\n\n";
  exit;
}


if(defined($opt_macro)) {
  eval "$opt_macro();";
  exit;
}


if(defined($opt_capture)){
  init_port();
  if($opt_capture =~ m/(\d)([AB])/){
    my $channel =$1;
    my $ab = $2;
    capture($channel,$ab);
  } else {
    die "wrong parameters to capture subroutine.\n";
  }
  exit;

}

if (defined($opt_plot)) {
  init_port();
  communicate("PLTDST=SRL"); # set scope plot output to serial interface
  plot();
  exit;
}


# no options were entered, print help screen
help();






##############################################
############## SUBROUTINES ###################
##############################################




GetOptions ('h|help'      => \$opt_help,
              'c|cmd=s'   => \$opt_command,
              'tty=s'     => \$ser_dev,
              'baud=s'    => \$baudrate,
              'capture=s' => \$opt_capture,
              'm|macro=s' => \$opt_macro,
              'plot'      => \$opt_plot,
              'q|quiet'   => \$opt_quiet,
              'show'      => \$opt_show,
              'pdf'       => \$opt_pdf
            );

sub help{
    print "
DSOCMD is a simple tool communicate with a GOULD 4094 DSO (digital storage oscilloscope)
via the serial interface. It is especially useful to export screenshots from the scope
as vector images or capture recorded trace data from the scope's memory.

written 2013 by Michael Wiebusch
acidbourbon.wordpress.com

    Usage: ./dsocmd.pl [-c \"COMMAND\" | -capture XX | -plot] [options]
   
options:
    [-h|--help]             : Show this help.
    [-tty /dev/yourDevice]  : sets the serial interface to /dev/yourDevice
                              instead of /dev/ttyUSB0
    [-baud BAUDRATE]        : sets the serial interface to BAUDRATE
    [-capture XX]           : downloads the trace data from channel XX (=1A,1B,2A,2B,...)
                              saves a dat file and a plot in ./capture
    [-plot]                 : make a screenshot of the scope and saves it in ./plot
    [-pdf]                  : saves the generated plots as pdf, use in combination with
                              -capture and -plot
    [-show]                 : shows the plot after a -plot or -capture
    [-c \"COMMAND\"]          : send \"COMMAND\" to the DSO and print the answer
    [-q]                    : quiet option, do not print debug data when sending a scope
                              command, use in combination with -c
examples:

    ./dsocmd -c \"HELLO\" -q -tty /dev/ttyUSB1 -baud 9600
    
    ./dsocmd -plot -pdf -show
    
    ./dsocmd -capture 1A -pdf -show
                                     
dependencies:

before you run the script, make sure you have the following software packages installed:

    libdevice-serialport-perl [ for serial communication, mandatory ]
    hp2xx [ for hpgl -> eps conversion ]
    texlive-font-utils [contains \"epstopdf\", for eps -> pdf conversion ]
    gnuplot [ for plots of downloaded traces ]

On a Debian/Ubuntu/Mint Linux you can install all that by typing this into your console:

\$ sudo apt-get install libdevice-serialport-perl hp2xx texlive-font-utils gnuplot

Make sure your user can access the serial interface. Therefore \"user\" has to be 
member of the \"dialout\" group. You can achieve this by simply typing:

\$ sudo usermod -a -G dialout user

Subsequently user has to log out and in again, so the changes become effective.
";
}




sub plot_request {
  
  $port->are_match(";");
  $port->lookclear; 
  $port->write("\nPLOT\n");
  
  my $data="";
  
  my $EOT_timeout=8; # seconds
  
  for (my $i = 0; ($i<$EOT_timeout*100) ;$i++) {
#     print $i."\n";
    while(my $a = $port->lookfor) {
       $i=0; # reset timeout
       print VERBOSE $a.";\n";
       $data.=$a.";\n";
       if ($a eq "AF") {
          print "transmission complete\n";
          $data =~ s/^.*PLOT\?//;
          return $data;
       }

    } 
      Time::HiRes::sleep(.01);

  }
  
  die "timeout\n";
  
}



sub communicate {

  my $ack_timeout=0.5;
  my $answer_timeout=10;

  my $command = $_[0];
  print VERBOSE "sending command $command\n";


  $port->are_match("\r");
  $port->lookclear; 
  $port->write("\n$command\n\n");
  
  my $ack = 0;




ACK_POLLING:  for (my $i = 0; ($i<$ack_timeout*100) ;$i++) {
#     print $i."\n";
    while(my $a = $port->lookfor) {
        if($a=~ m/[\?:]([^\?]+)/) {
          my $cmd_echo = $1;
          print VERBOSE "DSO received command $cmd_echo\n\n";
          if($cmd_echo ne $command) {
            print "ERROR: command transmission faulty\n";
            return "ERROR";
          }
          $ack=1;
          last ACK_POLLING;
        }

    } 
      Time::HiRes::sleep(.01);

  }
  
  unless($ack) {
    print "no answer\n";
    return "no answer";
  }
  
ANSWER_POLLING:  for (my $i = 0; ($i<$answer_timeout*100) ;$i++) {
#     print $i."\n";
    while(my $a = $port->lookfor) {

        print VERBOSE "received answer:\n";
        $a =~ s/\n//g; # remove empty lines
        print $a."\n";
        return $a;

    } 
      Time::HiRes::sleep(.01);

  }
  
  print "no answer :(\n";
  return "no answer";
  

}






sub init_port {


  # talk to the serial interface

  $port = new Device::SerialPort($ser_dev);
  unless ($port)
  {
    print "can't open serial interface $ser_dev\n";
    exit;
  }

  $port->user_msg('ON'); 
  $port->baudrate($baudrate); 
  $port->parity("none"); 
  $port->databits(8); 
  $port->stopbits(1); 
  $port->handshake("xoff"); 
  $port->write_settings;

}



sub getValue {
  my $valName=$_[0];
  my $answer = communicate($valName);
  if($answer =~ m/$valName=([^=]+)/){
    return $1;
  }
  die "could not retrieve desired value $valName!";
}


sub plot {

  my $plotDir = "./plots/";
  unless(-e $plotDir) {
    mkdir $plotDir;
  }
  
  my $hpglData = plot_request(); 
      my $baseFileName = "plot".strftime("_%Y-%m-%d_%H-%M-%S", localtime());
      my $hpglFile = $plotDir.$baseFileName.".hpgl";

      open(DATA,">$hpglFile");
      print DATA $hpglData;
      close(DATA);
      
#      system("hp2xx dualplot.hpgl -m eps -h150 -w200 -p542
#       chdir($plotDir);
      #system("hp2xx $hpglFile -m eps -p542 -a 2");
      system("hp2xx $hpglFile -m eps -p542  -a 2");
      #system("rm $hpglFile"); #delete hpglfile
      if ($opt_pdf) {
        system("epstopdf $hpglFile.eps --outfile=$plotDir$baseFileName.pdf && rm $hpglFile.eps");
      }
    if ($opt_show) {
      if(-e $plotDir.$baseFileName.".pdf") {
        system("xdg-open $plotDir$baseFileName.pdf");
      } else {
      system("xdg-open $hpglFile.eps");
      }
    }

}








sub capture {


my $captureDir = "./capture/";
my $channel = shift();
my $ab = shift();


my $transferCmd = "TRC$channel$ab";
my @data;
my @rawData;



my $timePerDiv= getValue("HS$ab");
my $screenWidthTime = $timePerDiv*10;

my $voltsPerDiv=getValue("VS$channel");
my $probeGain = getValue("PBG$channel");
$probeGain =~ s/^X//;
my $screenHeightVoltage= $voltsPerDiv*$probeGain*8;
my $traceOffset = getValue("VP$channel");
my $traceOffsetVoltage = $voltsPerDiv*$probeGain*$traceOffset;

print "\nwhole screen width: $screenWidthTime sec\n";
print "probe gain: $probeGain\n";
print "whole screen height: $screenHeightVoltage volts\n";
print "trace offset: $traceOffsetVoltage volts\n";





my $dataString = communicate($transferCmd);
# testdata if communication is too lengthy :D
# my $dataString = "TRC1A=-2,4,8,12,15,19,24,28,31,34,35,36,40,42,43,46,51,50,53,54,56,56,58,60,59,63,65,62,67,67,69,66,72,72,71,69,73,72,75,73,75,75,75,77,77,77,77,77,78,77,78,78,81,79,76,77,78,81,81,78,80,81,80,82,81,80,81,81,82,81,81,81,79,80,80,81,82,81,81,80,84,81,82,81,82,82,82,83,82,81,81,80,83,82,82,81,81,80,83,80,82,83,82,83,81,81,80,84,83,83,83,83,83,84,81,82,84,84,83,83,82,82,81,82,81,83,85,84,83,83,85,81,83,81,82,82,84,81,83,81,82,83,83,82,84,82,82,80,83,82,82,84,83,82,80,80,82,84,84,84,82,85,83,83,83,82,83,83,83,82,81,82,83,83,82,83,83,82,83,81,84,83,83,84,82,82,82,82,84,82,82,82,83,83,81,82,84,82,84,81,82,84,82,81,81,83,82,84,81,83,81,81,82,84,81,81,84,82,83,82,82,81,81,82,81,82,84,82,82,82,84,83,83,81,84,82,83,82,84,83,84,83,82,82,83,84,82,82,82,81,83,84,82,82,83,80,81,82,84,83,82,84,84,84,81,82,83,82,83,82,82,82,82,80,81,81,83,82,82,82,83,84,83,81,82,81,82,81,83,79,82,80,82,83,81,82,81,81,81,81,82,83,82,83,80,79,81,83,83,83,83,82,83,82,83,83,82,83,84,83,83,81,81,82,81,82,85,81,82,81,83,82,83,
# 82,82,81,82,82,82,82,82,82,81,82,82,82,82,81,82,81,82,84,80,82,79,79,78,83,83,85,82,82,82,82,83,82,82,83,83,82,83,82,81,82,81,83,83,81,82,83,85,82,83,82,82,81,82,81,83,82,82,82,81,82,82,81,81,80,82,81,81,82,83,82,81,80,78,85,85,82,82,82,83,83,82,83,82,82,83,81,83,82,82,84,81,81,83,81,83,82,83,82,82,81,81,81,83,82,82,80,81,83,81,83,84,81,82,81,82,80,82,83,81,82,81,81,78,84,82,82,83,82,81,82,80,81,82,82,83,83,82,81,81,82,81,81,83,82,76,67,58,50,43,36,28,20,16,9,4,-2,-8,-11,-14,-16,-22,-28,-31,-34,-35,-39,-40,-41,-44,-46,-52,-52,-55,-54,-56,-57,-59,-60,-60,-62,-63,-65,-65,-66,-66,-68,-69,-70,-71,-71,-74,-71,-72,-73,-73,-74,-74,-73,-76,-76,-75,-76,-76,-77,-77,-77,-76,-79,-77,-79,-80,-80,-78,-81,-79,-80,-79,-79,-79,-80,-82,-83,-82,-78,-79,-80,-80,-79,-80,-79,-81,-80,-79,-79,-79,-82,-81,-81,-80,-80,-83,-80,-80,-82,-82,-81,-80,-80,-80,-79,-81,-83,-79,-81,-81,-82,-82,-82,-81,-81,-80,-82,-82,-81,-82,-82,-81,-81,-80,-81,-83,-82,-82,-79,-81,-82,-80,-81,-80,-82,-82,-81,-82,-83,-81,-82,-81,-82,-82,-80,-82,-82,-80,-82,-
# 80,
# -82,-79,-80,-80,-81,-81,-82,-80,-81,-81,-82,-81,-82,-80,-80,-80,-80,-82,-82,-80,-83,-80,-80,-80,-82,-83,-82,-82,-80,-80,-81,-80,-80,-82,-81,-82,-82,-82,-82,-81,-80,-80,-83,-82,-82,-81,-81,-79,-81,-80,-80,-81,-82,-79,-79,-80,-79,-80,-82,-80,-82,-81,-81,-80,-80,-81,-80,-80,-82,-81,-83,-81,-79,-82,-81,-82,-83,-83,-78,-82,-80,-82,-81,-82,-81,-82,-83,-82,-79,-79,-81,-83,-80,-82,-81,-81,-81,-80,-82,-81,-80,-82,-82,-80,-79,-80,-81,-80,-82,-80,-83,-80,-80,-80,-81,-80,-82,-80,-81,-80,-83,-80,-81,-81,-80,-82,-82,-80,-80,-80,-80,-81,-81,-80,-82,-82,-80,-81,-82,-80,-80,-80,-80,-83,-81,-82,-80,-81,-81,-80,-80,-82,-80,-81,-81,-81,-81,-81,-81,-79,-80,-81,-80,-80,-80,-82,-81,-80,-80,-81,-81,-80,-80,-82,-82,-83,-81,-82,-80,-81,-82,-82,-82,-80,-81,-82,-83,-81,-82,-80,-82,-80,-82,-80,-80,-83,-82,-81,-81,-78,-80,-81,-80,-79,-78,-81,-81,-80,-81,-81,-81,-82,-80,-80,-81,-82,-80,-80,-83,-81,-82,-80,-80,-80,-80,-83,-80,-80,-82,-79,-82,-79,-80,-82,-80,-79,-82,-79,-80,-79,-80,-80,-80,-82,-81,-82,-80,-79,-79,-76,-80,-84,-82,-82,-81,-
# 83,
# -84,-81,-82,-83,-83,-82,-83,-82,-80,-81,-82,-82,-83,-81,-84,-80,-80,-82,-80,-83,-80,-83,-79,-79,-82,-80,-79,-83,-80,-80,-81,-81,-81,-81,-81,-84,-80,-82,-81,-83,-80,-80,-80,-80,-81,-81,-80,-78,-80,-80,-81,-80,-82,-78,-81,-81,-80,-79,-79,-81,-80,-81,-81,-80,-82,-80,-79,-79,-80,-82,-79,-79,-82,-80,-80,-78,-81,-81,-80,-81,-80,-80,-81,-80,-80,-79,-80,-81,-82,-81,-79,-80,-80,-79,-80,-80,-79,-78,-80,-80,-81,-77,-76,-71,-66,-61,-53,-47,-40,-35,-29,-21,-16,-10,-6,0,4,9,13,18,23,24,32";
# 
# 








if ($dataString =~ m/$transferCmd=([^=]+)/ ) {
  # execute if we have the right data format
  @rawData = split(",",$1);
  # calculate the correct values in volts and seconds ...
  my $timeCounter=0;
  push(@data,"#time [s]\t#voltage [V]");
  for my $byte (@rawData) {
    my $scaledVoltage =$byte/224*$screenHeightVoltage-$traceOffsetVoltage;
    my $timeIndex = $timeCounter/1007*$screenWidthTime;
    push(@data,"$timeIndex\t$scaledVoltage");
    $timeCounter++;
  
  }

} else {
    die "answer does not have correct format: $dataString\n\n";
}
      unless(-e $captureDir) {
        mkdir $captureDir;
      }
      my $baseFileName = $captureDir.$transferCmd.strftime("_%Y-%m-%d_%H-%M-%S", localtime());

      open(DATA,">$baseFileName.dat");
      print DATA join("\n",@data);
      close(DATA);

      open(GNUPLOT,"|gnuplot");
      if ($opt_pdf) {
      print GNUPLOT "set terminal postscript color solid\n";
      print GNUPLOT "set output \"|ps2pdf - $baseFileName.pdf\"\n";
      } else {
      print GNUPLOT "set terminal png\n";
      print GNUPLOT "set output \"$baseFileName.png\"\n";
      }
      print GNUPLOT qq%set xlabel "time [s]"\n%;
      print GNUPLOT qq%set ylabel "voltage [V]"\n%;
      my $minV=-$traceOffsetVoltage-$screenHeightVoltage/2;
      my $maxV=$minV+$screenHeightVoltage;
      print GNUPLOT qq%set yrange [$minV:$maxV]\n%;
#       print GNUPLOT "plot \"./data.dat\"\n";
      print GNUPLOT qq%plot '-' title "channel $channel$ab" w lines\n%;
      print GNUPLOT join("\n",@data);
      print GNUPLOT "\ne\n\n";
      close GNUPLOT;
      
      if ($opt_show) {
        if($opt_pdf) {
          system("xdg-open '$baseFileName.pdf'");
        } else {
          system("xdg-open $baseFileName.png");
        }
      }

}
