%global olm_version 3.2.13
%global commit 71f16b797fe47eb4d8ef64166d94942b6aa61da4
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name     : gomuks
Version  : 0.2.4
Release  : %{commit}
URL      : https://github.com/tulir/gomuks
Source0  : https://github.com/tulir/gomuks/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1  : https://gitlab.matrix.org/matrix-org/olm/-/archive/%{olm_version}/olm-%{olm_version}.tar.bz2
Summary  : A terminal based Matrix client written in Go.
Group    : Development/Tools
License  : GPLv3
BuildRequires : llvm
BuildRequires : go
BuildRequires : openssl-dev
BuildRequires : cmake

%description
A terminal based Matrix client written in Go.

%prep
%setup -q -n gomuks-%{commit} -a 1

%build
unset http_proxy
unset no_proxy 
unset https_proxy
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export CFLAGS="$CFLAGS -O3 -Ofast -falign-functions=32  -flto=auto -fno-semantic-interposition -fstack-protector-strong -mno-vzeroupper -mprefer-vector-width=256 "
export FCFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -flto=auto -fno-semantic-interposition -fstack-protector-strong -mno-vzeroupper -mprefer-vector-width=256 "
export FFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -flto=auto -fno-semantic-interposition -fstack-protector-strong -mno-vzeroupper -mprefer-vector-width=256 "
export CXXFLAGS="$CXXFLAGS -O3 -Ofast -falign-functions=32 -flto=auto -fno-semantic-interposition -fstack-protector-strong -mno-vzeroupper -mprefer-vector-width=256 "
export GOFLAGS='-buildmode=pie -v -trimpath'

pushd olm-%{olm_version}
cmake . -Bbuilddir -DCMAKE_BUILD_TYPE=Release
cmake --build builddir && cmake --install ./builddir --prefix /usr
  pushd ./builddir/tests/
    ctest .
  popd
popd
git config --global --add safe.directory /home
go build -v -ldflags "-extldflags '${LDFLAGS}'" .

%install
mkdir -p %{buildroot}/usr/lib64 && mv /usr/lib64/libolm* %{buildroot}/usr/lib64
install -Dm755 gomuks %{buildroot}/usr/bin/gomuks

%files
%defattr(-,root,root,-)
/usr/bin/gomuks
/usr/lib64/libolm*
