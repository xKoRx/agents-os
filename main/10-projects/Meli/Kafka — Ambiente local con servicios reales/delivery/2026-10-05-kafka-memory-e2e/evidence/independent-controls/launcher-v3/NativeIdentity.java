public final class NativeIdentity {
  public static void main(String[] arguments) throws Exception {
    ProcessHandle worker = ProcessHandle.current();
    ProcessHandle owner = worker.parent().orElseThrow();
    System.out.printf("{\"pid\":%d,\"birth\":\"%s\",\"owner_pid\":%d,\"owner_birth\":\"%s\"}%n",
        worker.pid(), worker.info().startInstant().orElseThrow(), owner.pid(), owner.info().startInstant().orElseThrow());
    System.out.flush();
    System.in.read();
  }
}
