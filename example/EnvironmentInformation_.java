package org.apache.flink.runtime.util;
import java.io.InputStream;
import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.lang.reflect.Method;
import java.util.List;
import java.util.Properties;
import org.apache.flink.util.OperatingSystem;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
public class EnvironmentInformation {
public static final String UNKNOWN = "<unknown>";
public static String getVersion() {
String version = EnvironmentInformation.class.getPackage().getImplementationVersion();
return version != null ? version : UNKNOWN;
}
public static RevisionInformation getRevisionInformation() {
String revision = UNKNOWN;
String commitDate = UNKNOWN;
try (InputStream propFile = EnvironmentInformation.class.getClassLoader().getResourceAsStream(".version.properties")) {
if (propFile != null) {
Properties properties = new Properties();
properties.load(propFile);
String propRevision = properties.getProperty("git.commit.id.abbrev");
String propCommitDate = properties.getProperty("git.commit.time");
revision = propRevision != null ? propRevision : UNKNOWN;
commitDate = propCommitDate != null ? propCommitDate : UNKNOWN;
}
} catch (Throwable t) {
} else {
}
}
return new RevisionInformation(revision, commitDate);
}
public static String getHadoopUser() {
try {
Class<?> ugiClass = Class.forName( "org.apache.hadoop.security.UserGroupInformation", false, EnvironmentInformation.class.getClassLoader());
Method currentUserMethod = ugiClass.getMethod("getCurrentUser");
Method shortUserNameMethod = ugiClass.getMethod("getShortUserName");
Object ugi = currentUserMethod.invoke(null);
return (String) shortUserNameMethod.invoke(ugi);
}
catch (ClassNotFoundException e) {
return "<no hadoop dependency found>";
}
catch (LinkageError e) {
}
catch (Throwable t) {
}
return UNKNOWN;
}
public static long getMaxJvmHeapMemory() {
final long maxMemory = Runtime.getRuntime().maxMemory();
if (maxMemory != Long.MAX_VALUE) {
return maxMemory;
} else {
final long physicalMemory = Hardware.getSizeOfPhysicalMemory();
if (physicalMemory != -1) {
return physicalMemory / 4;
} else {
throw new RuntimeException("Could not determine the amount of free memory.\n" + "Please set the maximum memory for the JVM, e.g. -Xmx512M for 512 megabytes.");
}
}
}
public static long getSizeOfFreeHeapMemoryWithDefrag() {
System.gc();
return getSizeOfFreeHeapMemory();
}
public static long getSizeOfFreeHeapMemory() {
Runtime r = Runtime.getRuntime();
return getMaxJvmHeapMemory() - r.totalMemory() + r.freeMemory();
}
public static String getJvmVersion() {
try {
final RuntimeMXBean bean = ManagementFactory.getRuntimeMXBean();
return bean.getVmName() + " - " + bean.getVmVendor() + " - " + bean.getSpecVersion() + '/' + bean.getVmVersion();
}
catch (Throwable t) {
return UNKNOWN;
}
}
public static String getJvmStartupOptions() {
try {
final RuntimeMXBean bean = ManagementFactory.getRuntimeMXBean();
final StringBuilder bld = new StringBuilder();
for (String s : bean.getInputArguments()) {
bld.append(s).append(' ');
}
return bld.toString();
}
catch (Throwable t) {
return UNKNOWN;
}
}
public static String[] getJvmStartupOptionsArray() {
try {
RuntimeMXBean bean = ManagementFactory.getRuntimeMXBean();
List<String> options = bean.getInputArguments();
return options.toArray(new String[options.size()]);
}
catch (Throwable t) {
return new String[0];
}
}
public static String getTemporaryFileDirectory() {
return System.getProperty("java.io.tmpdir");
}
public static long getOpenFileHandlesLimit() {
if (OperatingSystem.isWindows()) {
return -1L;
}
Class<?> sunBeanClass;
try {
sunBeanClass = Class.forName("com.sun.management.UnixOperatingSystemMXBean");
}
catch (ClassNotFoundException e) {
return -1L;
}
try {
Method fhLimitMethod = sunBeanClass.getMethod("getMaxFileDescriptorCount");
Object result = fhLimitMethod.invoke(ManagementFactory.getOperatingSystemMXBean());
return (Long) result;
}
catch (Throwable t) {
return -1L;
}
}
RevisionInformation rev = getRevisionInformation();
String version = getVersion();
String jvmVersion = getJvmVersion();
String[] options = getJvmStartupOptionsArray();
String javaHome = System.getenv("JAVA_HOME");
long maxHeapMegabytes = getMaxJvmHeapMemory() >>> 20;
String hadoopVersionString = getHadoopVersionString();
if (hadoopVersionString != null) {
} else {
}
if (options.length == 0) {
}
else {
for (String s: options) {
}
}
if (commandLineArgs == null || commandLineArgs.length == 0) {
}
else {
for (String s: commandLineArgs) {
}
}
}
}
public static String getHadoopVersionString() {
try {
Class<?> versionInfoClass = Class.forName( "org.apache.hadoop.util.VersionInfo", false, EnvironmentInformation.class.getClassLoader());
Method method = versionInfoClass.getMethod("getVersion");
return (String) method.invoke(null);
} catch (ClassNotFoundException | NoSuchMethodException e) {
return null;
} catch (Throwable e) {
return null;
}
}
private EnvironmentInformation() {}
public static class RevisionInformation {
public final String commitId;
public final String commitDate;
public RevisionInformation(String commitId, String commitDate) {
this.commitId = commitId;
this.commitDate = commitDate;
}
}
}
