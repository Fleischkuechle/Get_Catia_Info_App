using System;
using System.Diagnostics;

namespace PythonExecutableRunner
{
    /// <summary>
    /// This class provides methods to run a Python executable and parse its output.
    /// </summary>
    public class PythonExecutor
    {
        /// <summary>
        /// Runs a Python executable located at the specified path.
        /// Redirects the standard output and error streams to capture the output.
        /// 
        /// <param name="executablePath">The file path of the Python executable to run.</param>
        /// <returns>
        /// A Tuple containing the operating system, version, release, and service pack 
        /// as strings, or null if the execution fails.
        /// </returns>
        /// </summary>
        public static Tuple<string, string, string, string> RunPythonExecutable(string executablePath)
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = executablePath,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                var process = new Process { StartInfo = psi };
                process.Start();

                var output = process.StandardOutput.ReadToEnd();
                var error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (process.ExitCode != 0)
                {
                    Console.WriteLine($"Error running Python executable: {error}");
                    return null;
                }
                return ParseOutput(output);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to run Python executable: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// Parses the output of the Python executable.
        /// The output is expected to be in a specific format with each line containing 
        /// a key-value pair, separated by a colon.
        /// 
        /// <param name="output">The output string from the Python executable.</param>
        /// <returns>
        /// A Tuple containing the operating system, version, release, and service pack
        /// as strings, or null if parsing fails.
        /// </returns>
        /// </summary>
        private static Tuple<string, string, string, string> ParseOutput(string output)
        {
            try
            {
                string[] lines = output.Split(new[] { "\r\n", "\r", "\n" }, StringSplitOptions.RemoveEmptyEntries);
                string operatingSystem = lines[0].Split(':')[1].Trim();
                string version = lines[1].Split(':')[1].Trim();
                string release = lines[2].Split(':')[1].Trim();
                string servicePack = lines[3].Split(':')[1].Trim();

                return Tuple.Create(operatingSystem, version, release, servicePack);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to parse output: {ex.Message}");
                return null;
            }
        }
    }
}
