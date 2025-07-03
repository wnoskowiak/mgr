#
Neutrinos are electrically neutral, spin-½ elementary particles that belong to the lepton family within the Standard Model of particle physics. They exist in three distinct flavors, corresponding to the three charged leptons: the electron neutrino (νₑ), the muon neutrino (ν_μ), and the tau neutrino (ν_τ).

These flavor classifications arise from the weak decay processes mediated by the W boson, in which a charged lepton is produced alongside a corresponding neutrino. For instance, in a W⁻ decay producing an electron, an electron neutrino is emitted; similarly, decays yielding a muon or tau lepton produce a muon or tau neutrino, respectively.

Due to their lack of electric charge, negligible mass, and absence of color charge, neutrinos interact with matter only via the weak nuclear force. This interaction occurs through two fundamental mechanisms: neutral current interactions, mediated by the electrically neutral Z⁰ boson, and charged current interactions, mediated by the charged W⁺ or W⁻ bosons.

In charged current interactions, the neutrino exchanges a W boson with a target particle, resulting in the production of a charged lepton of the same flavor. In contrast, neutral current interactions involve the exchange of a Z⁰ boson and do not alter the identity of the interacting neutrino. 

Because weak interactions occur only at extremely short ranges—on the order of 10^−17 to 10^−18 meters — neutrinos pass largely undisturbed through space, making their detection a technical challange. Nevertheless studying the products of the aforementioned reactions form the primary means by which neutrinos can be detected and studied experimentally.

# neutrino detectors

## determining the type of the interacting neutrino

Neutral current (NC) interactions do not produce a charged lepton and thus provide no direct information about the neutrino’s flavor. charged current (CC) interactions however can be used to identify the flavor of the interacting neutrino.

Those types of interactions result in the production of a charged lepton of the same flavor as the neutrino. (*Interactions produce VUV scintilator potons*) These leptons can also interact with matter more eailsy when traveling through space.

By analyzing the interaction products, in conjunction with information gathered from the scintillation photons, it is possible to reconstruct the lepton’s trajectory and interaction point. This enables the determination of both the neutrino's flavor and the location of the interaction in space.


### Liquid Argon detectors

Liquid argon detectors comprise of a chamber filled with liqid argon. (say why argon - i think becouse its dense(?)) When a neutrino interacts with an argon nucleus, it produces charged particles that traverse the medium, leaving behind trails of ionized electrons. The detector volume is subjected to a uniform electric field, which causes these free electrons to drift toward a set of anode planes, where their arrival is recorded. Simultaneously, the interaction also generates vacuum ultraviolet (VUV) scintillation photons. These photons are detected by an array of scintillators strategically placed around the chamber, providing complementary timing and energy information. The combination of ionization charge collection and scintillation light detection allows for high-resolution, three-dimensional reconstruction of particle trajectories and interaction vertices within the detector volume.


-Large chamber filled in with a noble gas - in our case argon



-charged particles leave trails of ionizied electrons

- whole chamber is placed in an electric field - electrons travel to the anode

- they are detected along the way

- VUV scintillation photons are also emmited

- they are picked up by scintilators


## noise

- cosmic rays passing through the chamber can cause ionization

- this results in noise

- these noise patterns are very characteristic and are easy to recognize



## Microboone experiment

-MicroBooNN LArTPC is filled with Argon

- electric field is created by 




### MicroBooNE OpenSamples Dataset

The MicroBooNE OpenSamples dataset comprises two publicly available samples designed to facilitate research and development in neutrino physics and machine learning applications. Both samples feature simulated neutrino interactions from the Booster Neutrino Beam (BNB) overlaid onto real cosmic ray background data collected by the MicroBooNE detector. The first sample is inclusive, encompassing all neutrino flavors and interaction types occurring throughout the entire cryostat volume, with event distributions reflecting the experiment's nominal flux and cross-section models. The second sample focuses specifically on charged-current electron neutrino interactions within the active volume of the liquid argon time projection chamber (LArTPC). The datasets are provided in two formats: HDF5 and art/ROOT.

In further discussions we will focus only on the files containing wire info.

---

## Envirement preperation

The Jupyter notebooks accompanying the MicroBooNE OpenSamples repository recommend creating a Conda environment that includes the necessary packages. While there is nothing inherently wrong with this approach, it does introduce several disadvantages. Beyond general inefficiencies—such as longer environment loading times, higher memory usage, and increased disk space consumption—the most significant issue encountered was related to the sheer number of files generated by Conda distributions.

Both Conda and Miniconda installations can create and maintain hundreds of thousands of files. Although the total disk usage of these files is typically not problematic (many are symbolic links or small metadata files), the system used for processing data enforced strict quotas on the number of files each user could create. Installing a full Conda distribution brought the user account dangerously close to this limit, which severely impacted the usability of the system. For instance, launching a new Jupyter session became almost impossible, as nearly every action related to managing Jupyter generates additional log files, further pushing against the file quota.

Additionally, the environment setup proposed in the MicroBooNE OpenSamples notebooks depended on outdated libraries—most notably pynuml version 0.3, which is no longer maintained and is poorly documented. This package also requires an outdated version of Python (3.7) and depends on a deprecated version of HDF5. These constraints make it effectively impossible to use current versions of many essential packages, which significantly complicates the development process.

To address these issues and improve the portability and maintainability of the tools used for processing OpenSamples data, an alternative approach to environment management was adopted.

---

## Containarization and singularity

Containerization is a method of packaging software and its dependencies into isolated, self-contained units called containers. Each container includes all necessary binaries, libraries, and configuration files, ensuring that applications run consistently across different systems regardless of variations in the underlying infrastructure. Modern containerization solutions allow for building, distributing, and executing containers in a lightweight and reproducible manner. Containers are typically defined using a configuration file that builds on a base image and specifies additional dependencies and setup steps, producing a new image that can be versioned and reused.

In this specific case, a containerization tool called Singularity was used. Singularity is particularly well-suited for high-performance computing environments, as it enables users to define, build, and execute containers without requiring root privileges. A container definition file was created based on a modern Ubuntu base image. This definition specified the installation of all required dependencies and packages during the container build process. Using this approach made it possible to work with up-to-date software versions, including Python 3.9, the latest maintained release of the pynuml package, and a current version of HDF5, although these upgrades requires some code refactorings to be performed on the code present in open samples notebooks. Moreover, since the resulting container image is stored as a single file, this method also effectively circumvented the file quota limitations encountered with Conda-based setups.

---

## Image rendering

- script provided by microboone opensamples was used and modified (describe how these images were generated exactly - steps and all)
- images generated in greysacle, scaled down 2x for conviniece
- events were matched with data from the "xxxx" that included "..."
- combined into .csv manifest files

### Final image format

- how many pngs
- how many gbs

---

## Events present in the dataset

The BNB (Booster Neutrino Beam) sample contains a total of 24,332 events, all of which are classified as charged-current (CC) interactions. The dataset is composed exclusively of electron neutrinos and antineutrinos, with 19,448 events corresponding to neutrinos (PDG code 12) and 492 to antineutrinos (PDG code –12). No muon neutrinos (PDG 14 or –14) are present. The energy distribution of neutrino interactions in this sample has a mean value of 1.62 GeV, a median of 1.46 GeV, and a standard deviation of 0.86 GeV. The minimum recorded energy is 0.13 GeV, while the maximum reaches 6.13 GeV, with the interquartile range spanning from 0.96 to 2.11 GeV. These characteristics reflect a relatively high-energy subset of interactions, with consistent representation across the full energy spectrum.

The νₑ-enhanced sample consists of 19,940 events, containing a broader mix of neutrino types. The majority are muon neutrinos (23,984 with PDG 14), followed by smaller numbers of muon antineutrinos (208 with PDG –14), electron neutrinos (134 with PDG 12), and electron antineutrinos (6 with PDG –12). Of the total, 17,564 events are classified as charged-current, while 6,768 are neutral-current (NC) interactions. Within the charged-current subset, 17,457 events originate from muon neutrinos or antineutrinos, and 107 from electron neutrinos or antineutrinos, indicating a dominance of muon neutrino interactions in this sample. The energy distribution shows a mean of 1.20 GeV, median of 1.08 GeV, and standard deviation of 0.67 GeV, with values ranging from 0.06 GeV to 6.61 GeV, and the interquartile range spanning 0.80 to 1.42 GeV. This distribution suggests a slightly lower-energy spectrum on average, but with a broader mix of interaction types.


events sum - 44272

bnb -  24332

nue - 19940


in nue:

nu_pdg
 14    23984
-14      208
 12      134
-12        6

is_cc
1    17564
0     6768

Count of elements where 'nu_pdg' is 12 or -12 and 'is_cc' is 1: 107

Count of elements where 'nu_pdg' is 12 and 'is_cc' is 1: 101

Count of elements where 'nu_pdg' is 14 or -14 and 'is_cc' is 1: 17457

Count of elements where 'nu_pdg' is 14 and 'is_cc' is 1: 17338

Mean: 1.20076746086265
Median: 1.08149365
Standard Deviation: 0.6715692573171129
Min: 0.062644444
Max: 6.6122594

Summary Statistics:
count    24332.000000
mean         1.200767
std          0.671569
min          0.062644
25%          0.796795
50%          1.081494
75%          1.415627
max          6.612259
Name: nu_energy, dtype: float64

in bnb:

Mean: 1.6172239334483451
Median: 1.4605489
Standard Deviation: 0.860632415536723
Min: 0.1251314
Max: 6.132014

Summary Statistics:
count    19940.000000
mean         1.617224
std          0.860632
min          0.125131
25%          0.959046
50%          1.460549
75%          2.108691
max          6.132014
Name: nu_energy, dtype: float64


nu_pdg
 12    19448
-12      492
Name: count, dtype: int64


is_cc
1    19940
Name: count, dtype: int64

Count of elements where 'nu_pdg' is 12 or -12 and 'is_cc' is 1: 19940
Count of elements where 'nu_pdg' is 12 and 'is_cc' is 1: 19448
Count of elements where 'nu_pdg' is 14 or -14 and 'is_cc' is 1: 0
Count of elements where 'nu_pdg' is 14 and 'is_cc' is 1: 0

---

## CNN explenation

file:///C:/Users/wojte/Downloads/s13244-018-0639-9.pdf

Convolutional neural networks (CNNs) are a class of machine learning algorithms designed to automatically and adaptively learn spatial hierarchies of features, ranging from low-level edges to high-level semantic patterns. They consist of stacked convolutional and pooling layers responsible for feature extraction, followed by fully connected layers that perform the final classification. Each layer passes its output to the next, enabling progressively more abstract and complex features to be learned as information flows through the network.

## convolutional layer

### general mechanism

A convolution is a linear operation that involves element-wise multiplication between an input array and a corresponding kernel (also referred to as a filter), followed by summation of the resulting products. The kernel is an array of values of the same size as the input array, that defines the operation and characterizes the specific features being extracted.

In a convolutional layer, multiple such kernels are applied to every valid subsection of the input array with dimensions matching the kernel size. The result of each convolution is a single scalar value, which becomes an element of the output feature map. To preserve or control the spatial dimensions of the output, padding may be applied to the input array, typically by adding zeros around its border.

The output of a convolutional layer is an array (or tensor) with reduced spatial dimensions (depending on the padding and stride) and a number of channels equal to the number of kernels employed in the layer.

### feature recognition mechanism

During backpropagation, each element of every kernel is treated as a learnable parameter and is optimized using gradient descent. The gradients of these parameters are computed with respect to each input element (more precisely, with respect to each considered subsection of the input array). These gradients are then aggregated—typically by averaging—and the kernel parameters are updated accordingly.

The general objective is for the kernels to adjust themselves to specific features of the input image—that is, to produce high activation values when a particular feature is present and low values when it is absent. The calculated gradients for each subsection of the input array depend on the values of the inputs. Consequently, it is assumed that during training, the elements of the kernels are updated in such a way that each kernel learns to recognize a distinct feature in the input array.

## pooling layer

A pooling layer is a downsampling operation used to reduce the spatial dimensions of feature maps while preserving salient information. The specific pooling method used in each layer is selected based on its effectiveness for the given classification task (usually by trial and error). Among the available techniques, max pooling—which selects the maximum value within a specified region—is the most commonly employed approach.

Pooling layers operate independently on each channel and do not involve learnable parameters. By summarizing local regions, they can insure invaiance for small translation and reduce computational complexity in subsequent layers. Similar to convolutional layers, padding and stride can be used to control the spatial dimensions of the output.

## complete CNN

The first layers of the neural network consist of a hierarchy of convolution and pooling layers, each taking the output of the previous layer as input. The output of the final convolutional or pooling layer is then passed to a fully connected layer, which performs the final classification.

During training, the network first attempts to classify a batch of input elements. The predicted output is then compared to the true class labels, and a loss value is computed. This loss is subsequently backpropagated through the network, and the gradients for all learnable parameters are calculated. Finally, a step of gradient descent is performed, and the learnable parameters are updated accordingly.




## Further dataset processing

Although the final image dataset occupied approximately 13 GB on disk, this was primarily due to the use of compressed image formats (specifically, .png). When these images were loaded into memory as arrays of integers, their size increased dramatically—by more than a factor of 100 in some cases. It quickly became evident that the dataset was too large to be feasibly loaded into the system’s RAM without causing memory fragmentation. However, loading each image individually into memory incurred significant computational overhead: each image had to be read from disk, memory had to be allocated, and the image had to be decompressed before being converted into an array. Since training a convolutional neural network (CNN) typically requires each image to be loaded multiple times, it was crucial to minimize the number of image loading operations.

{Insert a chart comparing the total size of compressed images with the size of the same images loaded into memory as dense arrays.}

During development, it was observed that the processed images contained mostly empty (zero-value) pixels. While traces were present in all images, they typically occupied only a small portion of each image—approximately 5% of the total pixels. (Note: Mention that the threshold used during the generation of wire images was sufficiently low to eliminate noise.) As a result, the decision was made to represent the images using sparse arrays. Unlike dense arrays, where each element is stored explicitly in memory, sparse arrays assume a default value for all positions and store only the non-zero values along with their coordinates. Although these sparse arrays still need to be converted to dense format before being passed to the CNN, this conversion is significantly less costly than loading and decompressing images from disk. This optimization led to a substantial reduction in memory usage—by up to a factor of 70—making it feasible to load the entire dataset into RAM.

{Insert a chart comparing the total size of compressed images with the total memory usage of the sparse array representation.}

Another challenge arose from the number of individual files comprising the dataset. The final dataset contained approximately {(verify this number) 120,000} image files. This created issues similar to those previously encountered when working with Miniconda—namely, the system used for CNN training imposed quotas on the number of files each user could allocate. Operating under an account close to that limit proved to be cumbersome. Notably, the total dataset size remained well below the storage quota in terms of bytes, indicating that reducing the number of files could resolve the problem without affecting overall storage usage.

To address both issues, each .csv manifest file was loaded into a pandas DataFrame. Three additional columns were added to each record—one for each image associated with an event—and populated with the corresponding sparse arrays. Each resulting dataset was then saved as a single .pkl file, a format that preserves Python objects as they exist in memory. The combined size of all .pkl files was approximately {(verify this number) 32 GB}, which corresponds closely to the amount of memory required to load them into RAM.

---

## Convolutional neural networks

- ogólny opis CNNów - czym są, jak działają
- dyskusja dla czego mogą one być w tym przypadku użyteczne

---

- These types of networks are efficient at recognizing characteristical features in images

- the convolutional part can be trained to find features

- the fully conncected part can recognize combinations of those features

- that should technically be enough to recogize the types of interactions that took place within the detector

Convolutional neural networks (CNNs) are particularly effective at identifying characteristic features in images. The convolutional layers are responsible for learning and extracting these features, while the fully connected layers interpret combinations of them to perform classification. In the context of neutrino detection, this architecture is well-suited to recognizing patterns associated with specific types of interactions within the detector, making it a strong candidate for automated event identification.

-----

- Wanted to work with the simplest case

- Electron showers leave the most visible traces

- these only get created in charged current interactions of electron neutrino

- divide data into two classes - CC electron neutrino interactions and other.

----

- One can expect the higher energy neutrinos to be produce higher energy electron

- these cause more significant showers

- possibly easier to recognize 

- we narrow one dataset down to top 50% most energetic cases

To simplify the initial stages of analysis, the decision was made to focus on the most straightforward and visually distinct case: electron neutrino charged current (CC) interactions. These interactions produce energetic electrons that initiate electromagnetic showers, which leave highly visible and easily identifiable traces in the detector. Based on this, the dataset was divided into two classes—electron neutrino CC interactions and all other types of events. It was further hypothesized that higher-energy neutrinos are likely to produce more energetic electrons, which in turn generate more pronounced and spatially extended showers. Such events are presumed to be easier to detect and classify reliably. To leverage this property, the dataset was further narrowed down by selecting the top 50% most energetic electron neutrino CC events, thereby prioritizing those cases with the clearest and most informative signatures.



### Neural net - application in specific case

- training prep
- describe networks used
- describe label
- describe data
- "settings"