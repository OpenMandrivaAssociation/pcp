%define name	pcp	
%define	version	0.3.3
%define release	%mkrel 2
%define lib_name_orig	lib%{name}
%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define develname %mklibname -d %{name}

Summary:  	PCP is a tool for replicating files on multiple nodes of a PC cluster	
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/File transfer
URL:		http://www.cs.berkeley.edu/~bnc/pcp/
Source:		%{name}-%{version}.tar.bz2
Source1:	pcpd
Source2:	README.pcp
Patch0:		pcp-Makefile.in.patch
Requires:	openssh-clients, openssh-server, authd >= 0.2, xinetd, tftp
Provides:	%{name}-%{version}
Buildrequires:	libe-devel >= 0.2.1, authd-devel >= 0.2
Buildrequires:	openssl-devel
#Packager:       Antoine Ginies <aginies@mandrakesoft.com>
BuildRoot:	%{_tmppath}/%{name}-%{version}

%package	-n %{develname}
Summary:        Pcp devel package
Provides:       %{name}-devel-%{version}
Obsoletes:	%{lib_name}-devel
Group:          Development/Other

%description
pcp is a tool for replicating files on multiple nodes of a PC cluster. 
Replication is done by building an n-ary tree of TCP sockets and using 
parallelized, pipelined data transfers which use RSA authentication. 
For large file transfers or replication on many nodes, pcp provides highly 
efficient data transfers when compared to existing alternatives (e.g. NFS).

%description -n %{develname}
pcp devel package.

%prep
%setup -q
%patch0 -p0 -b .patch
cp %{SOURCE2} $RPM_BUILD_DIR/%{name}-%{version}/README

%build
%configure 
make

%install
rm -rf ${buildroot}

mkdir -p %{buildroot}/etc/xinetd.d
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%makeinstall 
install -m 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/xinetd.d/pcpd

%clean
rm -fr %{buildroot}

%post
# mise a jour /etc/services if needed
CHECK_PORT=`grep 2850 /etc/services`
if [ -z "$CHECK_PORT" ]; then
        echo "# Port needed by pcpd" >> /etc/services
        echo "pcp             2850/tcp                      # Caltech pcp" >> /etc/services
fi

service xinetd condrestart 

%postun
service xinetd condrestart 

%files
%defattr(-,root,root) 
%doc INSTALL ChangeLog AUTHORS README
%config(noreplace) %{_sysconfdir}/xinetd.d/pcpd
%{_bindir}/pcp
%{_sbindir}/pcpd

%files -n %{develname}
%defattr(-,root,root)
%doc INSTALL AUTHORS ChangeLog
%{_includedir}/pcp_lib.h
%{_libdir}/libpcp.a

