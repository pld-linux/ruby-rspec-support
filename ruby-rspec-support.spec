#
# Conditional build:
%bcond_without	doc		# don't build ri/rdoc

%define pkgname rspec-support
Summary:	Support utilities for RSpec modules
Summary(pl.UTF-8):	Narzędzia wspierające dla modułów RSpec
Name:		ruby-%{pkgname}
Version:	3.7.1
Release:	1
License:	MIT
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	a256e5c716dcb9a6877a037ab54997e3
Group:		Development/Languages
URL:		https://github.com/rspec/rspec-support
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
Requires:	ruby-thread_order >= 1.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RSpec::Support provides common functionality to RSpec::Core,
RSpec::Expectations and RSpec::Mocks.

%description -l pl.UTF-8
RSpec::Support udostępnia funkcjonalność wspólną dla RSpec::Core,
RSpec::Expectation i RSpec::Mocks.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
%{__mv} %{pkgname}-%{version}.gemspec %{pkgname}.gemspec
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

#'

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} ri/File/cdesc-File.ri
%{__rm} ri/Object/cdesc-Object.ri
%{__rm} ri/created.rid
%{__rm} ri/cache.ri
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog.md README.md
%dir %{ruby_vendorlibdir}/rspec
%{ruby_vendorlibdir}/rspec/support.rb
%{ruby_vendorlibdir}/rspec/support
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%dir %{ruby_ridir}/RSpec
%{ruby_ridir}/Object/command_from-i.ri
%{ruby_ridir}/Object/expected_encoding%3f-i.ri
%{ruby_ridir}/Object/have_successful_no_warnings_output-i.ri
%{ruby_ridir}/Object/load_all_files-i.ri
%{ruby_ridir}/RSpec/CallerFilter
%{ruby_ridir}/RSpec/Support
%{ruby_ridir}/RSpec/cdesc-RSpec.ri
%{ruby_ridir}/RSpecHelpers
%endif
